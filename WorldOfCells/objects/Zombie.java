public class Zombie extends Agent{
	private int vitesse;
	public static final double PSTEP= 0.09;
	private boolean time;
	
	public Zombie(int x, int y, int v){
		super(x,y);
		vitesse=v;
		time=false;
	}

	public void bite (ArrayList<Human> humans,ArrayList<Zombie> zombies){
		for(int i=humans.size()-1; i>=0;i--){
				Human h= humans.get(i);
				int xp=h.x;
				int yp=h.y;
				if ((xp==x)&&(yp==y)) {
					Zombie z = new Zombie(x,y);
					zombies.add(z);
					humans.remove(h);
				}
		}	
	}
	
	public void step(ArrayList<Human> humans,AgentsCA ca){
		for(int i=humans.size()-1; i>=0;i--){
			Human h= humans.get(i);
				int xp=h.x;
				int yp=h.y;
				if(h.alive && !h.bitten){
					if (x==xp){
						if((y - 1 + ca.getHeight()) % ca.getHeight()==y2){
							synchronized ( Buffer0 ) {
							agents.get(i).fuitS();
							}
						}
						if((y + 1 + ca.getHeight()) % ca.getHeight()==y2){
							synchronized ( Buffer0 ) {
							agents.get(i).fuitN();
							}
						
						}
					}
					if (y==yp){
					
						if((x + 1 + ca.getWidth()) % ca.getWidth()==x2){
							synchronized ( Buffer0 ) {
							agents.get(i).fuitO();
							}
						}
						if((x - 1 + ca.getWidth()) % ca.getWidth()==x2){
							synchronized ( Buffer0 ) {
							agents.get(i).fuitE();
							}
						
						}
					}
					
				}
		}
	}
	
	public void chaseN(){
			if (Math.random() > 0.1) // au hasard
				_orient = 0;

			// met a jour: la position de l'agent (depend de l'orientation)
			switch (_orient) {
			case 0: // nord	
				_y = (_y - 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 1: // est
				_x = (_x + 1 + _world.getWidth()) % _world.getWidth();
				break;
			case 2: // sud
				_y = (_y + 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 3: // ouest
				_x = (_x - 1 + _world.getWidth()) % _world.getWidth();
				break;
			}
	}
	public void chaseE(){
			if (Math.random() > 0.1) // au hasard
				_orient = 1;

			// met a jour: la position de l'agent (depend de l'orientation)
			switch (_orient) {
			case 0: // nord	
				_y = (_y - 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 1: // est
				_x = (_x + 1 + _world.getWidth()) % _world.getWidth();
				break;
			case 2: // sud
				_y = (_y + 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 3: // ouest
				_x = (_x - 1 + _world.getWidth()) % _world.getWidth();
				break;
			}
	}
	public void chaseS(){
			if (Math.random() > 0.1) // au hasard
				_orient = 2;

			// met a jour: la position de l'agent (depend de l'orientation)
			switch (_orient) {
			case 0: // nord	
				_y = (_y - 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 1: // est
				_x = (_x + 1 + _world.getWidth()) % _world.getWidth();
				break;
			case 2: // sud
				_y = (_y + 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 3: // ouest
				_x = (_x - 1 + _world.getWidth()) % _world.getWidth();
				break;
			}
	}
	public void chaseO(){
			if (Math.random() > 0.1) // au hasard
				_orient = 3;

			// met a jour: la position de l'agent (depend de l'orientation)
			switch (_orient) {
			case 0: // nord	
				_y = (_y - 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 1: // est
				_x = (_x + 1 + _world.getWidth()) % _world.getWidth();
				break;
			case 2: // sud
				_y = (_y + 1 + _world.getHeight()) % _world.getHeight();
				break;
			case 3: // ouest
				_x = (_x - 1 + _world.getWidth()) % _world.getWidth();
				break;
			}
	}
	
}
