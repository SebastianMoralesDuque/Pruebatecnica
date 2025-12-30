import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './components/templates/DashboardLayout';
import { LoginPage } from './pages/LoginPage';
import { EmpresasPage } from './pages/EmpresasPage';
import { ProductosPage } from './pages/ProductosPage';
import { InventarioPage } from './pages/InventarioPage';
import { UnauthorizedPage } from './pages/UnauthorizedPage';
import { AuthProvider, useAuth } from './context/AuthContext';

function AppContent() {
    const { auth, user } = useAuth();

    return (
        <Routes>
            <Route path="/login" element={!auth ? <LoginPage /> : <Navigate to="/empresas" />} />
            <Route path="/*" element={auth ? (
                <DashboardLayout user={user}>
                    <Routes>
                        <Route path="/empresas" element={<EmpresasPage />} />
                        <Route path="/productos" element={
                            <ProtectedRoute isAdminRequired={true}>
                                <ProductosPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/inventario" element={
                            <ProtectedRoute isAdminRequired={true}>
                                <InventarioPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/unauthorized" element={<UnauthorizedPage />} />
                        <Route path="*" element={<Navigate to="/empresas" />} />
                    </Routes>
                </DashboardLayout>
            ) : (
                <Navigate to="/login" replace />
            )} />
        </Routes>
    );
}

const ProtectedRoute = ({ children, isAdminRequired = false }) => {
    const { user } = useAuth();
    if (isAdminRequired && !user?.is_administrator) {
        return <UnauthorizedPage />;
    }
    return children;
};



function App() {
    return (
        <AuthProvider>
            <Router>
                <AppContent />
            </Router>
        </AuthProvider>
    );
}

export default App;
