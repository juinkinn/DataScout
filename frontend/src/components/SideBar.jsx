import { NavLink } from "react-router-dom";

export function Sidebar(){
  return (
    <div className="sidebar">
      <h2>DataScout</h2>
      <NavLink to="/datasets" className={({isActive})=>isActive?"active":""}>📊 Datasets</NavLink>
    </div>
  )
}