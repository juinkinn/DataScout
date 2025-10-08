import { useState,useEffect } from "react";
import { Sidebar } from "../components/SideBar.jsx";
import { Topbar } from "../components/TopBar.jsx";
import { DatasetCard } from "../components/DatasetCard.jsx";
import { CollectionCard } from "../components/CollectionCard.jsx";
import { getUserCollections, searchDatasets, importDataset, addToPostgres } from "../api/client";

export default function DatasetsPage({token,username,onLogout}){
  const [collections,setCollections]=useState([]);
  const [results,setResults]=useState([]);
  const [query,setQuery]=useState("");
  const [toast,setToast]=useState({msg:"",type:"success"});

  const loadCollections = async ()=>{
    try{ const data=await getUserCollections(token); setCollections(data); } 
    catch(err){ console.error(err);}
  }

  useEffect(()=>{ loadCollections(); },[]);

  const handleSearch = async ()=>{
    try{ const res = await searchDatasets(query); setResults(res); } 
    catch(err){ console.error(err);}
  }

  const handleAdd = async (ref)=>{
    try{
      await importDataset(ref, token);
      await addToPostgres(ref, token);
      setToast({msg:`Added ${ref}`,type:"success"});
      loadCollections();
      setTimeout(()=>setToast({msg:"",type:"success"}),3000);
    } catch(err){
      setToast({msg:"Failed: "+err.message,type:"error"});
      setTimeout(()=>setToast({msg:"",type:"success"}),3000);
    }
  }

  return (
    <div className="app">
      <Sidebar/>
      <div className="main">
        <Topbar username={username} onLogout={onLogout}/>
        <div className="content">
          <div className="search-bar">
            <input placeholder="Search datasets..." value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==="Enter"&&handleSearch()}/>
            <button onClick={handleSearch}>Search</button>
          </div>

          <div className="dataset-grid">
            {results.map(r=><DatasetCard key={r.ref} dataset={r} onAdd={handleAdd}/>)}
          </div>

          <h2 style={{marginTop:'24px'}}>📁 My Collections</h2>
          <div className="dataset-grid">
            {collections.length===0?<p>No datasets yet.</p>:collections.map(ds=><CollectionCard key={ds.dataset_ref} dataset={ds}/>)}
          </div>
        </div>
      </div>
      {toast.msg && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </div>
  )
}
