export default function Toast({ message, type }) {
  if (!message) return null;
  const color =
    type === "success" ? "bg-green-500" : type === "error" ? "bg-red-500" : "bg-gray-500";
  return (
    <div className={`fixed bottom-5 right-5 px-4 py-2 text-white rounded ${color} shadow-lg`}>
      {message}
    </div>
  );
}
