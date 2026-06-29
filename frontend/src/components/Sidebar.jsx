import {
  LayoutDashboard,
  BookOpen,
  FileText,
  Landmark,
  Wallet,
  TrendingUp,
  Bot,
  Settings,
} from "lucide-react";

const menu = [
  { icon: LayoutDashboard, title: "Dashboard" },
  { icon: BookOpen, title: "Trial Balance" },
  { icon: FileText, title: "Income Statement" },
  { icon: Landmark, title: "Balance Sheet" },
  { icon: Wallet, title: "Cash Flow" },
  { icon: TrendingUp, title: "Forecasting" },
  { icon: Bot, title: "AI Copilot" },
  { icon: Settings, title: "Settings" },
];

function Sidebar() {
  return (
    <aside className="w-72 bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-2xl font-bold">FinSight AI</h1>
        <p className="text-sm text-slate-400 mt-1">
          Enterprise FP&amp;A
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              className="flex items-center gap-3 w-full rounded-lg px-4 py-3 hover:bg-slate-800 transition"
            >
              <Icon size={20} />
              <span>{item.title}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;