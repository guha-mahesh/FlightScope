
import bird1 from './assets/bird1.png'
import bird2 from './assets/bird2.png'
import bird3 from './assets/bird3.png'
import bird4 from './assets/bird4.png'
import bird5 from './assets/bird5.png'

import Search from './components/Search'



const Home = () => {
  return (
    <>
      <img className = "bird bird1"src = {bird1} draggable="false"></img>
        <img className = "bird bird2"src = {bird2} draggable="false"></img>
        <img className = "bird bird3"src = {bird3} draggable="false"></img>
        <img className = "bird bird4"src = {bird4} draggable="false"></img>
        <img className = "bird bird5"src = {bird5} draggable="false"></img>
    <div className = "HomeScreen">
      <div className = "content">
      <h1>FlightScope</h1>
     
        <Search/>

       

</div>


    </div>
    </>
  )
}

export default Home