import React from 'react';

export const LoadingSpinner = ({ size = 20 }) => (
    <div
        className="animate-spin rounded-full border-2 border-white/10 border-t-white"
        style={{ width: size, height: size }}
    />
);
