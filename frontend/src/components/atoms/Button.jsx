import React from 'react';
import { LoadingSpinner } from './LoadingSpinner';

export const Button = ({ children, loading, variant = 'primary', className = '', ...props }) => {
    const baseStyles = "font-semibold py-3 px-6 rounded-xl transition-all duration-300 active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2";

    const variants = {
        primary: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/20",
        secondary: "bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10",
        danger: "bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20",
        success: "bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20",
        glass: "glass-card hover:bg-white/10 text-white"
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${className}`}
            disabled={loading || props.disabled}
            {...props}
        >
            {loading ? <LoadingSpinner size={20} /> : children}
        </button>
    );
};
