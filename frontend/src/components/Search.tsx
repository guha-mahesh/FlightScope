

import { useEffect, useState } from 'react'
import SearchItem from "./SearchItem";


const backendURL = import.meta.env.VITE_BACKEND_URL

interface species{
    species: string;
    id: number;
}

const Search = () => {

    const [species, setSpecies] = useState<species[]| null>(null)
    const [query, setQuery] = useState("")


    useEffect(()=>{

        const fetchSpecies = async ()=>{
            const response = await fetch(`${backendURL}/birds/species`)
            const data = await response.json();
            setSpecies(data)

        }


        fetchSpecies();



    }, [backendURL])


    const filteredSpecies = species?.filter((s) =>
    s.species
  .toLowerCase()
  .replace(/[-\s]/g, "") 
  .includes(
    query.toLowerCase().replace(/[-\s]/g, "")
  )
  );
  return (



<div className = "fullSearch">

    <div className ="Search">

      <input className = "searchbox" value={query} placeholder = "What bird are you looking to see?" onChange = {(e)=>setQuery(e.target.value)}></input>


       



    </div>
    <div className= "results">
       {query && filteredSpecies?.map((s, index) => (
          <SearchItem key={index} id = {s.id} species={s.species}>

          </SearchItem>
        ))}


    </div>
    
      </div>
  )
}

export default Search