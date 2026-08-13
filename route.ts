import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: NextRequest) {
  try {
    const { image, purchasePrice, shippingEstimate, additionalCosts } = await req.json();

    if (!image) {
      return NextResponse.json({ error: 'Image is required' }, { status: 400 });
    }

    // This is the prompt that instructs the AI to be cautious and structured.
    const prompt = `
      Analyze this item for a reseller. 
      Identify the brand, model, category, era, and material.
      Assess the condition based on the photo.

      IMPORTANT: Estimate its resale value on platforms like eBay, Mercari, and Facebook Marketplace.
      Be cautious. Use ranges. Do NOT state specific sold prices unless you are certain.
      If you are unsure of the brand or model, say "Unknown".

      Calculate financials based on:
      - Purchase Price: $${purchasePrice || 0}
      - Est. Shipping Cost: $${shippingEstimate || 0}
      - Additional Costs: $${additionalCosts || 0}
      - Assume platform fees are roughly 13%.

      Return ONLY a JSON object in this exact format:
      {
        "identification": { "category": "", "brand": "", "model": "", "era": "", "material": "", "confidence": 0.0 },
        "condition": "",
        "estimatedValue": { "low": 0, "typical": 0, "high": 0 },
        "verdict": "BUY" | "MAYBE" | "PASS",
        "reasoning": "",
        "listing": { "title": "", "description": "", "condition": "", "askingPrice": 0, "minimumPrice": 0 }
      }
    `;

    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: prompt },
            { type: "image_url", image_url: { url: image } },
          ],
        },
      ],
      response_format: { type: "json_object" },
    });

    const aiData = JSON.parse(response.choices[0].message.content || '{}');

    // Financial calculations
    const typicalValue = aiData.estimatedValue.typical;
    const fees = typicalValue * 0.13;
    const net = typicalValue - fees - (shippingEstimate || 0) - (additionalCosts || 0);
    const profit = net - (purchasePrice || 0);
    const roi = (purchasePrice || 0) > 0 ? (profit / purchasePrice) * 100 : 0;

    const result = {
      ...aiData,
      financials: {
        purchasePrice: Number(purchasePrice) || 0,
        estimatedFees: Number(fees.toFixed(2)),
        estimatedShipping: Number(shippingEstimate) || 0,
        estimatedNet: Number(net.toFixed(2)),
        estimatedProfit: Number(profit.toFixed(2)),
        roi: Number(roi.toFixed(1)),
      }
    };

    return NextResponse.json(result);
  } catch (error: any) {
    console.error('Analysis error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
