import { Bell, Search, UserCircle } from "lucide-react";

function Topbar() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">

      <div className="flex items-center gap-3 bg-slate-100 rounded-lg px-4 py-2 w-96">
        <Search size={18} className="text-slate-500" />

        <input
          type="text"
          placeholder="Search accounts, reports..."
          className="bg-transparent outline-none w-full"
        />
      </div>

      <div className="flex items-center gap-6">

        <button className="relative">
          <Bell size={22} />
        </button>

        <div className="flex items-center gap-3">
          <UserCircle size={34} />

          <div>
            <p className="font-semibold">Joseph Abuya</p>
            <p className="text-xs text-slate-500">
              Financial Analyst
            </p>
          </div>
        </div>

      </div>

    </header>
  );
}

export default Topbar;