import React from 'react';

export const Input = ({ icon: Icon, className = '', ...props }) => {
    return (
        <div className="relative w-full">
            <input
                className={`input-field ${Icon ? 'pl-12' : ''} ${className}`}
                {...props}
            />
            {Icon && (
                <Icon
                    className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
                    size={20}
                />
            )}
        </div>
    );
};
