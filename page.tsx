'use client';

import React, { useState, useRef } from 'react';
import { X, Camera, RefreshCw, ChevronRight, Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function ScanPage() {
  const router = useRouter();
  const [image, setImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [costs, setCosts] = useState({ purchase: '', shipping: '' });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const analyze = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image,
          purchasePrice: costs.purchase,
          shippingEstimate: costs.shipping
        }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      const sessionData = { ...data, image, id: Date.now().toString(), createdAt: new Date().toISOString() };
      sessionStorage.setItem('last_scan', JSON.stringify(sessionData));
      router.push('/result');
    } catch (err) {
      alert('Analysis failed. Check console.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col">
      <header className="p-4 flex justify-between items-center">
        <button onClick={() => router.back()} className="p-2"><X /></button>
        <span className="font-bold">FLIPFINDER SCAN</span>
        <div className="w-10"></div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center p-6 gap-6">
        <div className="w-full aspect-square bg-slate-800 rounded-3xl overflow-hidden border-2 border-dashed border-slate-700 flex items-center justify-center relative">
          {image ? (
            <>
              <img src={image} className="w-full h-full object-cover" />
              <button onClick={() => setImage(null)} className="absolute top-4 right-4 bg-black/50 p-2 rounded-full"><RefreshCw size={20} /></button>
            </>
          ) : (
            <button onClick={() => fileInputRef.current?.click()} className="flex flex-col items-center gap-2 text-slate-500">
              <Camera size={48} />
              <span className="font-bold">Tap to capture or upload</span>
            </button>
          )}
        </div>

        <input type="file" accept="image/*" capture="environment" ref={fileInputRef} onChange={handleCapture} className="hidden" />

        {image && (
          <div className="w-full space-y-4 animate-in fade-in slide-in-from-bottom-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-[10px] font-bold uppercase text-slate-500">Buy Price</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-bold">$</span>
                  <input 
                    type="number" 
                    placeholder="0.00"
                    value={costs.purchase}
                    onChange={e => setCosts({...costs, purchase: e.target.value})}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 pl-7 font-bold focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="space-y-1">
                <label className="text-[10px] font-bold uppercase text-slate-500">Est. Ship Cost</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-bold">$</span>
                  <input 
                    type="number" 
                    placeholder="0.00"
                    value={costs.shipping}
                    onChange={e => setCosts({...costs, shipping: e.target.value})}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 pl-7 font-bold focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            <button 
              onClick={analyze}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 p-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 shadow-lg transition-all"
            >
              {loading ? <Loader2 className="animate-spin" /> : 'ANALYZE ITEM'}
              {!loading && <ChevronRight />}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
