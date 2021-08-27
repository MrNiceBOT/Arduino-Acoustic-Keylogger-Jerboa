int setSize;
int numSets;

int graphBorder = 35;

int maxSets = 191;
int maxPoints = 393;

ArrayList<Slider> characterSliders;

Slider points_slider;
Slider sets_slider;

int update = -1;

ArrayList<ArrayList<Set>> sets;

/**
 * Initialise sliders and import initial datasets.
 */
void setup(){
    fullScreen();
    background(255);
    textAlign(CENTER, CENTER);
    
    characterSliders = new ArrayList();
    for (int i = 0; i < 4; i++){
        characterSliders.add(new Slider(20, 2*i*height/8 + height/8, 
            150, 16, 0, 25, true));
    }
    
    points_slider = new Slider("Points: ", 20, 40, 60, 10, 
        10, maxPoints, false);
    sets_slider = new Slider("Sets: ", 110, 40, 60, 10, 10, 
        maxSets, false);
    
    setSize = (int) points_slider.getValue();
    numSets = (int) sets_slider.getValue();
    
    sets = new ArrayList();
    for (int i = 0; i < 4; i++){
        sets.add(generateSets("data/" + 
            characterSliders.get(i).getValueChar() + ".txt"));
    }
    
    for (int i = 0, j = 0; i < height; i+=height/4, j++){
        drawSets(sets.get(j), 200, width, i, i+height/4);
    }
}

/**
 * Redraw graphs on updates and draw sliders.
 */
void draw(){
    for (Slider slider : characterSliders){
         slider.display();   
    }
    
    points_slider.display();
    sets_slider.display();
    
    if (update != -1){
        if (update != 5){
            sets.set(update, generateSets("data/" + 
                characterSliders.get(update).getValueChar() + ".txt"));
        }
        
        background(255);
        for (int i = 0, j = 0; i < height; i+=height/4, j++){
            drawSets(sets.get(j), 200, width, i, i+height/4);
        }
        update =- 1;
    }
}

/**
 * Press all sliders when mouse pressed.
 */
void mousePressed(){
    for (Slider slider : characterSliders){
         slider.press();   
    } 
    
    points_slider.press();
    sets_slider.press();
}

/**
 * Check what needs updating when key released.
 */
void mouseReleased(){
    for (Slider slider : characterSliders){
         slider.release();   
    }
    
    if (points_slider.release()){
        setSize = (int) points_slider.getValue();
        update = 5;
    }
    
    if (sets_slider.release()){
        numSets = (int) sets_slider.getValue();
        update = 5;
    }
    
    if (mouseY < height/4){
        update = 0;
    } else if (mouseY < height/2){
        update = 1;
    } else if (mouseY < 3*height/4){
        update = 2;
    } else {
        update = 3;
    }
}

/**
 * Draws the list of sets on the graph.
 */
void drawSets(ArrayList<Set> sets, int left, 
        int right, int bottom, int top){
    int max = 0;
    
    for (int i = 0; i < numSets; i++){
        for (int j = 0; j < setSize; j++){
            int val = sets.get(i).Points.get(j);
            
            if (val > max)
                max = val;
        }
    }
    
    for (int i = 0; i < numSets; i++){
         Set set = sets.get(i);
         set.display(left, right, bottom, top, max);   
    }
    
    stroke(255, 0, 0);
    strokeWeight(4);
    
    strokeWeight(1);
    stroke(0);
    fill(0);

    strokeWeight(1);
    
    line(left + graphBorder, top - graphBorder, 
        left + graphBorder, bottom + graphBorder);
    line(left + graphBorder, top - graphBorder, 
        right - 2.5*graphBorder, top - graphBorder);
}

/**
 * Generates a list of Sets from the data stored in file 
 * at given path.
 */
ArrayList<Set> generateSets(String filename){
    ArrayList<Set> toReturn = new ArrayList();
    String[] strings = loadStrings(filename);
    
    for (int i = 0; i < strings.length; i++){
        ArrayList<Integer> set = new ArrayList();
        
        String currentLine = strings[i];
        String curInt = "";
        
        for (int j = 0; j < currentLine.length(); j++){
            try{
                while(currentLine.charAt(j) != ' '){
                    curInt += 
                        Character.toString(currentLine.charAt(j));
                    j++;
                }
            } catch (Exception StringIndexOutOfBoundsException){
                currentLine = strings[i++];
            }
            
            if (!curInt.equals("")){
                set.add(Integer.parseInt(curInt));
                curInt = "";
            }
        } 
        
        toReturn.add(new Set(set));
    }
    
    return toReturn;
}

/**
 * Class that holds a set of points to plot.
 */
class Set {
    ArrayList<Integer> Points;
    int col;
    
    Set(ArrayList<Integer> Points){
         this.Points = Points;   
         this.col = (int) random(0, 255);
    }
    
    void display(int left, int right, int bottom, int top, 
            int max){
        strokeWeight(1);
        colorMode(HSB);
        stroke(col, 255, 150);
        
        for (int i = 0; i < setSize-1; i++){
            line(map(i,0, setSize-1, left + graphBorder, 
                    right - graphBorder), 
                map(Points.get(i), max, 0, bottom+graphBorder, 
                    top-graphBorder), 
                map(i+1,0, setSize-1, left + graphBorder, 
                    right - graphBorder), 
                map(Points.get(i+1), max, 0, bottom+graphBorder, 
                    top-graphBorder));
        }    
        stroke(0);
        colorMode(RGB);
    }
}
