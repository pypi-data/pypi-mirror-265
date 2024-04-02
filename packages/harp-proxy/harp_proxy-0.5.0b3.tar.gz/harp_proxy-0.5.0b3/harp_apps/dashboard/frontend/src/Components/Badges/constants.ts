export const apdexScale: { label: string; threshold?: number; className: string }[] = [
  { label: "A++", threshold: 98, className: "bg-teal-400" },
  { label: "A+", threshold: 96, className: "bg-emerald-400" },
  { label: "A", threshold: 93, className: "bg-green-500" },
  { label: "B", threshold: 83, className: "bg-lime-500" },
  { label: "C", threshold: 69, className: "bg-yellow-500" },
  { label: "D", threshold: 49, className: "bg-amber-500" },
  { label: "E", threshold: 31, className: "bg-orange-500" },
  { label: "F", threshold: 17, className: "bg-red-500" },
  { label: "G", className: "bg-red-700" },
]
