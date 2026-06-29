import useFilters from "../hooks/useFilters";

function FilterBar({ filters }) {
    const {
        year,
        setYear,
        quarter,
        setQuarter,
        month,
        setMonth,
        country,
        setCountry,
    } = useFilters();

    return (
        <div className="bg-white rounded-xl shadow p-5">

            <div className="grid grid-cols-4 gap-4">

                <select
                    className="border rounded-lg p-2"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                >
                    <option value="">All Years</option>

                    {filters.years.map((y) => (
                        <option key={y} value={y}>
                            {y}
                        </option>
                    ))}

                </select>

                <select
                    className="border rounded-lg p-2"
                    value={quarter}
                    onChange={(e) => setQuarter(e.target.value)}
                >
                    <option value="">All Quarters</option>

                    {filters.quarters.map((q) => (
                        <option key={q} value={q}>
                            {q}
                        </option>
                    ))}

                </select>

                <select
                    className="border rounded-lg p-2"
                    value={month}
                    onChange={(e) => setMonth(e.target.value)}
                >
                    <option value="">All Months</option>

                    {filters.months.map((m) => (
                        <option key={m} value={m}>
                            {m}
                        </option>
                    ))}

                </select>

                <select
                    className="border rounded-lg p-2"
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                >
                    <option value="">All Countries</option>

                    {filters.countries.map((c) => (
                        <option key={c} value={c}>
                            {c}
                        </option>
                    ))}

                </select>

            </div>

        </div>
    );
}

export default FilterBar;
