import { Brain } from "lucide-react";

function VarianceNarrative({ narrative }) {
    if (!narrative || narrative.length === 0) return null;

    return (
        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl p-6 text-white">
            <div className="flex items-center gap-3 mb-4">
                <div className="bg-white/20 h-10 w-10 rounded-lg flex items-center justify-center">
                    <Brain size={20} />
                </div>
                <div>
                    <h3 className="font-semibold">Variance Insights</h3>
                    <p className="text-xs text-white/70">What the pattern suggests</p>
                </div>
            </div>

            <ul className="space-y-3">
                {narrative.map((point, idx) => (
                    <li key={idx} className="flex gap-3 text-sm text-white/95 leading-relaxed">
                        <span className="text-white/50">—</span>
                        <span>{point}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default VarianceNarrative;
