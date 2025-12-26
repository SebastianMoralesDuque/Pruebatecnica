import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Hash, Key, Cloud, Loader2 } from 'lucide-react';

const steps = [
    { title: "Generando Hash", description: "Creando huella criptográfica...", icon: Hash },
    { title: "Firmando Transacción", description: "Autorizando con llave privada...", icon: Key },
    { title: "Sello en Solana", description: "Publicando prueba en mainnet/devnet...", icon: Cloud },
];

export const BlockchainLoader = ({ currentStep = 0 }) => {
    return (
        <div className="space-y-6 py-4">
            <div className="flex flex-col items-center justify-center mb-8">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                    className="text-indigo-500 mb-4"
                >
                    <Loader2 size={40} />
                </motion.div>
                <h3 className="text-xl font-bold text-white">Certificación en progreso</h3>
                <p className="text-sm text-muted">Asegurando la integridad de tus datos...</p>
            </div>

            <div className="space-y-4">
                {steps.map((step, idx) => {
                    const Icon = step.icon;
                    const isActive = idx === currentStep;
                    const isCompleted = idx < currentStep;

                    return (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0.3 }}
                            animate={{
                                opacity: isActive ? 1 : (isCompleted ? 0.8 : 0.3),
                                scale: isActive ? 1.02 : 1
                            }}
                            className={`flex items-center gap-4 p-4 rounded-2xl border transition-colors ${isActive ? 'bg-indigo-500/10 border-indigo-500/30' : 'bg-white/5 border-white/5'
                                }`}
                        >
                            <div className={`p-2 rounded-xl ${isActive ? 'bg-indigo-500 text-white' : (isCompleted ? 'bg-emerald-500 text-white' : 'bg-white/10 text-muted')
                                }`}>
                                <Icon size={20} />
                            </div>
                            <div className="flex-1">
                                <h4 className={`text-sm font-bold ${isActive ? 'text-indigo-100' : 'text-slate-400'}`}>
                                    {step.title}
                                </h4>
                                <p className="text-[11px] text-muted">
                                    {idx === currentStep ? step.description : (isCompleted ? '¡Completado!' : 'Esperando...')}
                                </p>
                            </div>
                            {isCompleted && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="text-emerald-500"
                                >
                                    <Cloud size={16} />
                                </motion.div>
                            )}
                        </motion.div>
                    );
                })}
            </div>
        </div>
    );
};
