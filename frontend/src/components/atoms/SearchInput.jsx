import React from 'react';
import { Search } from 'lucide-react';

export const SearchInput = ({ value, onChange, placeholder = "Buscar..." }) => (
    <div className="relative w-full md:w-64">
        <input
            type="text"
            className="w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all text-slate-200 placeholder:text-slate-500"
            placeholder={placeholder}
            value={value}
            onChange={onChange}
        />
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" size={18} />
    </div>
);
