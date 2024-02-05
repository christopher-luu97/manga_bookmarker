import "./App.css";
import "./assets/fonts/fonts.css";
import { Header } from "./components/Header";
import { Footer } from "./components/Footer";
import { ApplicationContent } from "./components/ApplicationContent";

function App() {
  return (
    <div className="App">
      <Header />
      <ApplicationContent />
      <Footer />
    </div>
  );
}

export default App;
