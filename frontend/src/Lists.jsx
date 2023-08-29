import {useEffect, useState} from "react";
import { useOutletContext } from "react-router-dom";

const Lists = () => {
    const [lists, setLists] = useState([]);
    const [apiFetch] = useOutletContext();

    useEffect(() => {
        const fetchData = async () => {
            const response = await apiFetch('grouplist');
            setLists(response.data);
        }
        fetchData();
        // console.log(lists)
    }, [])

    useEffect(() => {
        // This effect watches for changes in the 'lists' state variable
        // console.log(lists);
      }, [lists]); // Include 'lists' as a dependency

    return (
    <main className="Lists">
        <h2>Your Lists</h2>
        <br />
        {lists.map((list)=>{
            return (
            <div>
                <p>{list.name}</p>
                <p>{list.group.name}</p>
                <br />
            </div>
            )
        })}
    </main>
    )

    
}

export default Lists