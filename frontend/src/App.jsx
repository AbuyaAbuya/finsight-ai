import Router from "./router";
import { FilterProvider } from "./contexts/FilterContext";

function App() {
    return (
        <FilterProvider>
            <Router />
        </FilterProvider>
    );
}

export default App;
