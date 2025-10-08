export function Topbar({username,onLogout}){
  return (
    <div className="topbar">
      <span>Welcome, {username}</span>
      <button onClick={onLogout}>Logout</button>
    </div>
  )
}