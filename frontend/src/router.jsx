import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "./layouts/AppLayout";

import Dashboard from "./pages/Dashboard";
import TrialBalance from "./pages/TrialBalance";
import IncomeStatement from "./pages/IncomeStatement";
import BalanceSheet from "./pages/BalanceSheet";
import CashFlow from "./pages/CashFlow";
import Forecast from "./pages/Forecast";
import AICopilot from "./pages/AICopilot";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/trial-balance"
            element={<TrialBalance />}
          />

          <Route
            path="/income-statement"
            element={<IncomeStatement />}
          />

          <Route
            path="/balance-sheet"
            element={<BalanceSheet />}
          />

          <Route
            path="/cash-flow"
            element={<CashFlow />}
          />

          <Route
            path="/forecast"
            element={<Forecast />}
          />

          <Route
            path="/ai-copilot"
            element={<AICopilot />}
          />

          <Route
            path="*"
            element={<Navigate to="/" replace />}
          />

        </Route>
      </Routes>
    </BrowserRouter>
  );
}