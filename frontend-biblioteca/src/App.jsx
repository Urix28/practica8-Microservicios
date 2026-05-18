import { useState, useEffect } from 'react'

function App() {
  const [catalogo, setCatalogo] = useState({});
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  const API_URL = "https://pratica7-pwa-production.up.railway.app";

  // Cargar el catálogo al iniciar
  const obtenerCatalogo = async () => {
    try {
      const res = await fetch(`${API_URL}/api/catalogo`);
      const data = await res.json();
      setCatalogo(data);
    } catch (err) {
      console.error("Error al conectar con la API:", err);
    }
  };

  useEffect(() => {
    obtenerCatalogo();
  }, []);

  const solicitarPrestamo = async (titulo) => {
    setCargando(true);
    setMensaje("");
    try {
      const res = await fetch(`${API_URL}/api/prestar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titulo })
      });
      const data = await res.json();
      
      setMensaje(data.mensaje);
      obtenerCatalogo(); // Recargar stock tras el préstamo
    } catch (err) {
      setMensaje("Error de conexión con el servicio.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      {/* Header Institucional */}
      <header className="bg-ipn-guinda text-white p-6 shadow-lg">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Biblioteca ESCOM</h1>
          <span className="bg-white text-ipn-guinda px-3 py-1 rounded-full text-sm font-bold">
            PWA
          </span>
        </div>
      </header>

      <main className="container mx-auto p-6">
        {/* Notificaciones */}
        {mensaje && (
          <div className={`mb-6 p-4 rounded-lg text-white font-medium text-center shadow-md ${
            mensaje.includes("exitoso") ? "bg-green-500" : "bg-red-500"
          }`}>
            {mensaje}
          </div>
        )}

        {/* Rejilla de Libros */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(catalogo).map(([titulo, stock]) => (
            <div key={titulo} className="bg-white p-6 rounded-xl shadow-sm border-t-4 border-ipn-guinda flex flex-col justify-between transition-transform hover:scale-105">
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{titulo}</h3>
                <p className="text-gray-600 mb-4">
                  Disponibles: <span className={`font-bold ${stock > 0 ? "text-green-600" : "text-red-600"}`}>
                    {stock}
                  </span>
                </p>
              </div>
              
              <button
                onClick={() => solicitarPrestamo(titulo)}
                disabled={stock === 0 || cargando}
                className={`w-full py-3 rounded-lg font-bold text-white transition-colors ${
                  stock > 0 
                  ? "bg-ipn-guinda hover:bg-opacity-90 active:bg-red-900" 
                  : "bg-gray-400 cursor-not-allowed"
                }`}
              >
                {stock > 0 ? "Solicitar Préstamo" : "No disponible"}
              </button>
            </div>
          ))}
        </div>
      </main>

      <footer className="text-center text-gray-500 p-8">
        Práctica 7 PWA - Riveros González Armando Uriel
      </footer>
    </div>
  )
}

export default App