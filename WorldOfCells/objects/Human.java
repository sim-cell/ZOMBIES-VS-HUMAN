public class Human extends Agent{
	private boolean hunger;
	private boolean alive;
	//private int health;
	private boolean thirsty;
	private boolean bitten;
	private int vitesse;
	private int age;
	private int gun;
	public static final double PREP=0.1;
	public static final double PNOISE=0.2;
	public static final double PHIDE=0.4;
	//public static final double PCONFLICT=0.4;

	
	public Human(int x, int y){
		super(x,y);
		hunger=false;
		alive=true;
		thirsty=false;
		bitten=false;
		age=0;
		gun=0;
	}
	
	public Human(int x, int y, int a, int g){
		super(x,y);
		hunger=false;
		alive=true;
		thirsty=false;
		bitten=false;
		age=a;
		gun=g;
	}
	
	public Human reproduction(){
		if(Math.rand()<PREP && age>18){
			Human baby= new Human (this.x, this.y);
		}
		return baby;
	}
	
}
