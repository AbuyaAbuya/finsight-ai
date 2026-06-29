import { createContext, useContext, useMemo, useState } from "react";

const FilterContext = createContext(null);

export function FilterProvider({ children }) {
  const [year, setYear] = useState("");
  const [quarter, setQuarter] = useState("");
  const [month, setMonth] = useState("");
  const [country, setCountry] = useState("");
  const [region, setRegion] = useState("");

  const value = useMemo(
    () => ({
      year,
      setYear,

      quarter,
      setQuarter,

      month,
      setMonth,

      country,
      setCountry,

      region,
      setRegion,
    }),
    [year, quarter, month, country, region]
  );

  return (
    <FilterContext.Provider value={value}>
      {children}
    </FilterContext.Provider>
  );
}

export function useFilterContext() {
  const context = useContext(FilterContext);

  if (!context) {
    throw new Error(
      "useFilterContext must be used inside FilterProvider."
    );
  }

  return context;
}
