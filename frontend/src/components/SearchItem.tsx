
import { useNavigate } from "react-router-dom";


interface props{
    species: string;
    id: number;

}

const SearchItem = ({species, id}: props) => {
    const navigate = useNavigate();

  return (
    <div className = "searchItem" onClick = {()=>{navigate(`/bird/${id}`)}}>


        {species}
    </div>
  )
}

export default SearchItem