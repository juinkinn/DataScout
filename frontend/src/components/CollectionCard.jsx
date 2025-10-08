export function CollectionCard({dataset}){
  return (
    <div className="card">
      <strong>{dataset.dataset_ref}</strong>
      <br/>
      <a href={`https://www.kaggle.com/datasets/${dataset.dataset_ref}`} target="_blank">View</a>
    </div>
  )
}