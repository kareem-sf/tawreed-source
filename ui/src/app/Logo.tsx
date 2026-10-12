// Neutral package placeholder, authored for this MIT candidate; no brand geometry or font outlines.
export function Logo({ size = 22 }: { size?: number }) {
  return <svg width={size} height={size} viewBox="0 0 256 256" aria-hidden="true" data-testid="logo"><rect x="24" y="24" width="208" height="208" rx="24" fill="#64748b" /><path d="M72 80h112v96H72zM72 112h112M112 80v96" fill="none" stroke="#fff" strokeWidth="12" /></svg>;
}
