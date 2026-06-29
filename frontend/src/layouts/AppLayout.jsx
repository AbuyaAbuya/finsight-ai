import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

function AppLayout() {

    return (

        <div className="h-screen flex bg-slate-100">

            {/* Sidebar */}

            <Sidebar />

            {/* Content */}

            <div className="flex-1 flex flex-col overflow-hidden">

                {/* Header */}

                <Topbar />

                {/* Main */}

                <main className="flex-1 overflow-y-auto">

                    <div className="max-w-[1800px] mx-auto px-10 py-8">

                        <Outlet />

                    </div>

                </main>

            </div>

        </div>

    );

}

export default AppLayout;