public class Animal extends Agent{
	public static final double PREP =0.4;
	public Animal(int x, int y){
		super(x,y);
	}
	
	public Animal reproduction(){
		if(Math.rand()<PREP && age>18){
			Animal baby= new Human (this.x, this.y);
		}
		return baby;
	}

}
