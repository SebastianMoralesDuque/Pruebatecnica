import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertCircle } from 'lucide-react';

export const Feedback = ({ type, message, className = '' }) => {
    if (!message) return null;

    const styles = type === 'success'
        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
        : 'bg-red-500/10 text-red-400 border border-red-500/20';

    const Icon = type === 'success' ? CheckCircle : AlertCircle;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className={`p-4 rounded-xl flex items-center gap-3 mb-6 ${styles} ${className}`}
            >
                <Icon size={20} />
                <span className="text-sm font-medium">{message}</span>
            </motion.div>
        </AnimatePresence>
    );
};
