import { useState } from 'react';
import { Check, Calendar, MapPin, Activity, AlertCircle, Wind } from 'lucide-react';
import { Button } from './components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Popover, PopoverContent, PopoverTrigger } from './components/ui/popover';
import { Calendar as CalendarComponent } from './components/ui/calendar';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';

function App() {
  const [date, setDate] = useState(new Date());
  const [city, setCity] = useState('Santiago');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const cities = ['Santiago', 'Puerto Montt', 'Puerto Varas', 'Valparaíso', 'Viña del Mar'];

  const getAirQualityLevel = (pm25Value) => {
    if (pm25Value <= 12) return { level: 'Bom', color: 'text-green-500', bg: 'bg-green-100' };
    if (pm25Value <= 35.4) return { level: 'Moderado', color: 'text-yellow-500', bg: 'bg-yellow-100' };
    if (pm25Value <= 55.4) return { level: 'Prejudicial para grupos sensíveis', color: 'text-orange-500', bg: 'bg-orange-100' };
    if (pm25Value <= 150.4) return { level: 'Prejudicial', color: 'text-red-500', bg: 'bg-red-100' };
    if (pm25Value <= 250.4) return { level: 'Muito prejudicial', color: 'text-purple-500', bg: 'bg-purple-100' };
    return { level: 'Perigoso', color: 'text-red-700', bg: 'bg-red-200' };
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);

    try {
      const formattedDate = format(date, 'yyyy-MM-dd');
      const response = await fetch(`http://127.0.0.1:8080/forecast_pm25?city=${city}&date=${formattedDate}`);
      
      if (!response.ok) {
        throw new Error('Falha ao obter previsão');
      }
      
      const data = await response.json();
      if (data.length > 0) {
        setPrediction(data[0]);
      } else {
        throw new Error('Nenhuma previsão disponível para esta data.');
      }
    } catch (err) {
      setError(err.message);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center bg-gradient-to-r from-blue-500 to-purple-600">
      <div className="container mx-auto max-w-md">
        <Card className="shadow-xl">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold">Previsão de PM2.5</CardTitle>
            <CardDescription>Consulte a qualidade do ar para diferentes cidades do Chile</CardDescription>
          </CardHeader>
          
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2">
                  <MapPin className="h-4 w-4" /> Cidade
                </label>
                <Select value={city} onValueChange={(value) => setCity(value)}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Selecione uma cidade" />
                  </SelectTrigger>
                  <SelectContent>
                    {cities.map((cityName) => (
                      <SelectItem key={cityName} value={cityName}>
                        {cityName}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2">
                  <Calendar className="h-4 w-4" /> Data
                </label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button variant="outline" className="w-full justify-start text-left font-normal">
                      {format(date, 'PPP', { locale: ptBR })}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <CalendarComponent
                      mode="single"
                      selected={date}
                      onSelect={(date) => date && setDate(date)}
                      locale={ptBR}
                    />
                  </PopoverContent>
                </Popover>
              </div>
              
              <Button 
                className="w-full" 
                onClick={handlePredict} 
                disabled={loading}
              >
                {loading ? 'Consultando...' : 'Consultar Previsão'}
              </Button>
              
              {error && (
                <div className="p-3 rounded bg-red-100 text-red-700 flex items-center gap-2">
                  <AlertCircle className="h-4 w-4" />
                  {error}
                </div>
              )}
              
              {prediction && (
                <div className="mt-6 space-y-4">
                  <div className="text-center">
                    <h3 className="text-lg font-medium">
                      Resultado para {city} em {format(date, 'dd/MM/yyyy')}
                    </h3>
                  </div>
                  
                  <div className="flex justify-center">
                    <div className={`p-6 rounded-full ${getAirQualityLevel(prediction.qt_pm25).bg}`}>
                      <span className="text-3xl font-bold">
                        {prediction.qt_pm25.toFixed(1)}
                      </span>
                      <span className="text-sm"> µg/m³</span>
                    </div>
                  </div>
                  
                  <div className="bg-white p-4 rounded-lg shadow-sm border">
                    <div className="flex items-center gap-2 mb-2">
                      <Activity className="h-5 w-5" />
                      <span className="font-semibold">Qualidade do ar:</span>
                      <span className={`font-medium ${getAirQualityLevel(prediction.qt_pm25).color}`}>
                        {getAirQualityLevel(prediction.qt_pm25).level}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Wind className="h-5 w-5" />
                      <span className="font-semibold">Recomendação:</span>
                      <span className="text-gray-700">
                        {prediction.qt_pm25 > 35.4 ? 
                          'Evite atividades ao ar livre' : 
                          'Qualidade adequada para atividades externas'}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default App;
