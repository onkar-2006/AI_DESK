import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { motion } from 'framer-motion';
import { Send, Bot, Truck, ShoppingBag, ShieldCheck, Headset, Phone, Package, User, Sparkles } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(uuidv4());
  const [activeOrder, setActiveOrder] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { id: Date.now(), role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const { data } = await axios.post('http://localhost:8000/chat', {
        user_id: 101,
        session_id: sessionId,
        query: input
      });

      if (data.response.toLowerCase().includes("order")) {
        setActiveOrder({ id: "BK-7702", status: "In Transit", driver: "Suresh P." });
      }

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        sentiment: data.sentiment_detected
      }]);
    } catch (e) {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        role: 'assistant', 
        content: "System Offline: Connect your FastAPI backend to port 8000." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#020617] text-slate-100 overflow-hidden font-sans">
      
      {/* SIDEBAR: DARK GLASS LOOK */}
      <aside className="w-80 bg-[#0f172a] border-r border-slate-800 hidden lg:flex flex-col">
        <div className="p-6 border-b border-slate-800 bg-[#1e293b]/50">
          <div className="flex items-center gap-2 font-bold text-xl text-indigo-400">
            <Sparkles size={24} fill="currentColor" /> <span>Lux AI</span>
          </div>
          <p className="text-slate-500 text-[10px] mt-1 uppercase tracking-widest font-black">Midnight Support v2</p>
        </div>
        
        <div className="p-6 flex-1 space-y-8 overflow-y-auto">
          <section>
            <h3 className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-4">Tracking Context</h3>
            {activeOrder ? (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} 
                className="bg-indigo-500/10 border border-indigo-500/20 rounded-2xl p-4 shadow-2xl">
                <div className="flex justify-between items-start mb-3">
                  <span className="bg-indigo-500 text-[9px] px-2 py-0.5 rounded-full font-bold text-white uppercase">Active</span>
                  <Truck size={16} className="text-indigo-400" />
                </div>
                <p className="text-xs text-slate-400">Order #{activeOrder.id}</p>
                <p className="text-sm font-bold text-white mt-1">{activeOrder.status}</p>
                <div className="mt-3 pt-3 border-t border-slate-800 flex items-center gap-2 text-[11px] text-slate-400">
                  <User size={12} className="text-indigo-400"/> <span>{activeOrder.driver}</span>
                </div>
              </motion.div>
            ) : (
              <div className="border-2 border-dashed border-slate-800 rounded-3xl p-8 text-center bg-slate-900/20">
                <Package className="mx-auto text-slate-700 mb-2" size={32} />
                <p className="text-xs text-slate-500">Mention an order to see its status</p>
              </div>
            )}
          </section>

          <section>
            <h3 className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-4">Quick Actions</h3>
            <button className="w-full flex items-center gap-3 text-sm text-slate-400 p-3 rounded-xl hover:bg-slate-800 transition border border-transparent hover:border-slate-700">
              <Headset size={18} className="text-indigo-400"/> Request Human
            </button>
          </section>
        </div>

        <div className="p-4 bg-emerald-500/5 m-4 rounded-2xl border border-emerald-500/10 flex items-center gap-2 text-emerald-500 text-[10px] font-bold">
          <ShieldCheck size={16} /> DATA PROTECTION ACTIVE
        </div>
      </aside>

      {/* MAIN CHAT AREA */}
      <main className="flex-1 flex flex-col bg-[#020617]">
        <header className="h-20 bg-[#020617]/80 backdrop-blur-xl border-b border-slate-800 flex items-center px-8 justify-between sticky top-0 z-20">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-2xl shadow-indigo-500/20 rotate-3">
              <Bot size={28} className="-rotate-3" />
            </div>
            <div>
              <h2 className="font-bold text-white text-lg tracking-tight">Smart Assistant</h2>
              <p className="text-[10px] text-emerald-400 font-bold uppercase tracking-tighter flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span> Neural Link Online
              </p>
            </div>
          </div>
        </header>

        {/* CHAT MESSAGES */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center opacity-10">
              <Bot size={80} className="mb-4" />
              <p className="font-medium text-xl">How can I help today?</p>
            </div>
          )}
          {messages.map((msg) => (
            <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] p-4 rounded-2xl shadow-xl relative ${
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white rounded-tr-none' 
                  : 'bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none'
              }`}>
                {msg.sentiment === 'Angry' && (
                  <div className="absolute -top-3 left-0 bg-rose-600 text-white text-[9px] px-2 py-0.5 rounded-full font-black shadow-lg">
                    CRITICAL ISSUE
                  </div>
                )}
                <p className="text-sm leading-relaxed">{msg.content}</p>
              </div>
            </motion.div>
          ))}
          {loading && (
            <div className="flex gap-1.5 p-4 bg-slate-900 w-fit rounded-2xl border border-slate-800">
              <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce"></div>
              <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>

        {/* DARK INPUT AREA */}
        <div className="p-8 bg-[#020617] border-t border-slate-800">
          <div className="max-w-4xl mx-auto flex items-center gap-4 bg-slate-900/50 p-2 rounded-2xl border border-slate-800 focus-within:border-indigo-500/50 transition-all group">
            <input 
              className="flex-1 bg-transparent border-none outline-none px-4 py-2 text-sm text-slate-200 placeholder:text-slate-600"
              placeholder="Ask about orders, returns, or technical support..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button 
              onClick={sendMessage}
              className="bg-indigo-600 text-white p-3 rounded-xl hover:bg-indigo-500 transition-all shadow-lg active:scale-95 group-hover:shadow-indigo-500/20"
            >
              <Send size={20} />
            </button>
          </div>
          <p className="text-center text-[9px] text-slate-700 mt-4 uppercase tracking-[3px]">Secure Artificial Intelligence Interface</p>
        </div>
      </main>
    </div>
  );
};

export default App;