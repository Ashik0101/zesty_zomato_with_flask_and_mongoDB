import "./App.css";
import Home from "./pages/HomePage";
import { Route, Routes } from "react-router-dom";
import UserMenuPage from "./pages/UserMenuPage";

function App() {
  return (
    <div className="App">
      <>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/orders" element={<UserMenuPage />}></Route>
        </Routes>
      </>
    </div>
  );
}

export default App;
