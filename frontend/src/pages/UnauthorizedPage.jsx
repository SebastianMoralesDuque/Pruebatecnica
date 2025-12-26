import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ShieldAlert, LayoutDashboard } from 'lucide-react';

export const UnauthorizedPage = () => (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
        <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-red-500/10 p-8 rounded-full text-red-500 mb-8"
        >
            <ShieldAlert size={80} />
        </motion.div>
        <h2 className="text-4xl font-bold mb-4">Acceso Restringido</h2>
        <p className="text-muted text-lg max-w-md mb-8">
            Lo sentimos, tu cuenta no tiene los privilegios necesarios para acceder a esta sección.
            Contacta con un administrador si crees que esto es un error.
        </p>
        <Link to="/empresas" className="btn-primary flex items-center gap-2">
            <LayoutDashboard size={20} />
            Volver al Panel Principal
        </Link>
    </div>
);
