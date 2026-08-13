export interface Identification {
  category: string;
  brand: string;
  model: string;
  era: string;
  material: string;
  confidence: number;
}

export interface Financials {
  purchasePrice: number;
  estimatedFees: number;
  estimatedShipping: number;
  estimatedNet: number;
  estimatedProfit: number;
  roi: number;
}

export interface AnalysisResult {
  id: string;
  image: string;
  identification: Identification;
  condition: string;
  estimatedValue: {
    low: number;
    typical: number;
    high: number;
  };
  financials: Financials;
  verdict: 'BUY' | 'MAYBE' | 'PASS';
  reasoning: string;
  listing: {
    title: string;
    description: string;
    condition: string;
    askingPrice: number;
    minimumPrice: number;
  };
  createdAt: string;
}
