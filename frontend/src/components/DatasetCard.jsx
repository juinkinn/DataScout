export function DatasetCard({dataset,onAdd}){
  return (
    <div className="card">
      <h3>{dataset.title}</h3>
      <a href={`https://www.kaggle.com/datasets/${dataset.ref}`} target="_blank">View</a>
      <button onClick={()=>onAdd(dataset.ref)}>Add</button>
    </div>
  )
}