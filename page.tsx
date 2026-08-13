'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AnalysisResult } from '@/types';
import { ChevronLeft, Trash2, TrendingUp, DollarSign, Calendar } from 'lucide-react';

export default function InventoryPage() {
  const router = useRouter();
  const [items, setItems] = useState<AnalysisResult[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem('ff_inventory');
    if (saved) setItems(JSON.parse(saved));
  }, []);

  const deleteItem = (id: string) => {
    const updated = items.filter(i => i.id !== id);
    setItems(updated);
    localStorage.setItem('ff_inventory', JSON.stringify(updated));
  };

  return (
    <div className="max-w-md mx-auto min-h-screen bg-slate-50">
      <header className="p-4 flex justify-between items-center bg-white border-b sticky top-0 z-10">
        <button onClick={() => router.push('/')} className="p-2"><ChevronLeft /></button>
        <span className="font-black tracking-tight">MY INVENTORY</span>
        <div className="w-10"></div>
      </header>

      <main className="p-4 space-y-4">
        {items.length === 0 ? (
          <div className="text-center py-20 text-slate-400">
            <p className="font-bold">Inventory is empty.</p>
            <p className="text-sm">Scan an item to get started.</p>
          </div>
        ) : (
          items.map(item => (
            <div key={item.id} className="bg-white rounded-2xl overflow-hidden shadow-sm border flex">
              <div className="w-24 h-24 shrink-0">
                <img src={item.image} className="w-full h-full object-cover" />
              </div>
              <div className="flex-1 p-3 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-sm line-clamp-1">{item.identification.brand} {item.identification.model}</h4>
                    <p className="text-[10px] text-slate-400 font-bold uppercase">{item.identification.category}</p>
                  </div>
                  <button onClick={() => deleteItem(item.id)} className="text-slate-300 hover:text-red-500"><Trash2 size={16} /></button>
                </div>
                <div className="flex justify-between items-end">
                  <div className="flex gap-3">
                    <div className="text-center">
                      <p className="text-[8px] font-black text-slate-400 uppercase">Profit</p>
                      <p className="text-xs font-black text-green-600">${item.financials.estimatedProfit}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[8px] font-black text-slate-400 uppercase">ROI</p>
                      <p className="text-xs font-black text-blue-600">{item.financials.roi}%</p>
                    </div>
                  </div>
                  <span className={clsx(
                    "px-2 py-0.5 rounded-full text-[8px] font-black uppercase",
                    item.verdict === 'BUY' ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"
                  )}>
                    {item.verdict}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </main>
    </div>
  );
}

function clsx(...classes: any[]) {
  return classes.filter(Boolean).join(' ');
}
