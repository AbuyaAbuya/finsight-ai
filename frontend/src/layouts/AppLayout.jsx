import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

function AppLayout() {
  return (
    <div className="flex h-screen bg-slate-100">

      <Sidebar />

      <div className="flex flex-col flex-1 overflow-hidden">

        <Topbar />

        <main className="flex-1 overflow-auto p-8">
          <Outlet />
        </main>

      </div>

    </div>
  );
}

export default AppLayout;