import React from 'react';
import { Shield, CheckCircle, Info } from 'lucide-react';
import { motion } from 'framer-motion';

export const IntegrityInfo = () => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-6 rounded-3xl border-emerald-500/20 bg-emerald-500/5 mt-4"
        >
            <div className="flex items-start gap-4">
                <div className="p-2 bg-emerald-500/20 rounded-xl text-emerald-400">
                    <Shield size={20} />
                </div>
                <div>
                    <h4 className="text-sm font-bold text-emerald-100 mb-1 flex items-center gap-2">
                        ¿Qué es la Integridad Blockchain?
                    </h4>
                    <p className="text-xs text-emerald-300/70 leading-relaxed mb-3">
                        Al certificar, generamos una huella digital única (Hash) de tu inventario y la sellamos en Solana.
                    </p>
                    <ul className="space-y-2">
                        <li className="flex items-center gap-2 text-[11px] text-emerald-200/80">
                            <CheckCircle size={12} className="text-emerald-500" />
                            <span><strong>Inmutable:</strong> Los datos no pueden borrarse ni alterarse.</span>
                        </li>
                        <li className="flex items-center gap-2 text-[11px] text-emerald-200/80">
                            <CheckCircle size={12} className="text-emerald-500" />
                            <span><strong>Auditable:</strong> Cualquiera puede verificar la prueba on-chain.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </motion.div>
    );
};
