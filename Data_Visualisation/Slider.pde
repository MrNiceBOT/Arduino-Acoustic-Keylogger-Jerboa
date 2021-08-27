/**
 * This class implements a slider that can be used by the user to 
 * select a value.
 */
class Slider {
    int startX, startY, sliderWidth, sliderHeight;
    float minVal, maxVal;
    int labelSize;
    float sliderX;
    int currentVal;
    String label;
    boolean sliderPressed = false;
    boolean character_select;
    String display = "";

    // Constructor
    Slider(int startX, int startY, int sliderWidth, 
            int sliderHeight, float minVal, 
            float maxVal, boolean character_select) {
        this.startX = startX;
        this.startY = startY;
        this.sliderWidth = sliderWidth;
        this.sliderHeight = sliderHeight;
        this.minVal = minVal;
        this.maxVal = maxVal;
        this.character_select = character_select;

        this.currentVal = (int)(minVal + maxVal) / 2;

        sliderX = startX + sliderWidth / 2;
    }
    
    // Overloaded constructor for displayname
    Slider(String display, int startX, int startY, 
            int sliderWidth, int sliderHeight, 
            float minVal, float maxVal, 
            boolean character_select) {
        this.startX = startX;
        this.startY = startY;
        this.sliderWidth = sliderWidth;
        this.sliderHeight = sliderHeight;
        this.minVal = minVal;
        this.maxVal = maxVal;
        this.character_select = character_select;
        this.display = display;

        this.currentVal = (int)(minVal + maxVal) / 2;

        sliderX = startX + sliderWidth / 2;
    }

    // Returns the value of the slider
    float getValue() {
        return currentVal;
    }
    
    // Return the character associated with stored value
    char getValueChar() {
        return (char) (currentVal + 97);   
    }

    // Draws the slider on the sketch
    void display() {
        noStroke();
        if (sliderPressed) {
            press();
        }

        fill(200);
        rect(startX - sliderHeight / 2, startY, 
            sliderWidth + sliderHeight, sliderHeight, 
            sliderHeight);

        fill(100);
        rect(sliderX - sliderHeight / 2, startY, sliderHeight, 
            sliderHeight, sliderHeight);
        
        fill(255);
        rect(startX, startY - 75, sliderWidth, 75);
        
        if (character_select){
            textSize(48);
            fill(0);
            text(getValueChar(), startX + sliderWidth/2, startY - 50);
        } else {
            textSize(11);
            fill(0);
            text(display + (int) getValue(), startX + sliderWidth/2, 
                startY - 25);
        }
    }

    // Checks if the slider has been clicked
    void press() {
        if (mouseX > startX && mouseX < startX + sliderWidth) {
            if (mouseY > startY && mouseY < startY + sliderHeight || 
                    sliderPressed) {
                sliderPressed = true;
            }
        }

        if (sliderPressed) {
            if (mouseX <= startX + sliderWidth && mouseX >= startX) {
                sliderX = mouseX;
                currentVal = Math.round(map(mouseX, startX, 
                    startX + sliderWidth, minVal, maxVal));
                return;
            } else if (mouseX > startX + sliderWidth) {
                sliderX = startX + sliderWidth;
                currentVal = Math.round(maxVal);
                return;
            } else if (mouseX < startX) {
                sliderX = startX;
                currentVal = Math.round(minVal);
                return;
            }
        }
    }

    // Releases the slider so the value change stops
    boolean release() {
        if (sliderPressed){
            sliderPressed = false;
            return true;
        }
        sliderPressed = false;
        return false;
    }

    // Updates the position of the slider
    void update() {
        sliderPressed = true;
        sliderX = mouseX;
        currentVal = (int) map(mouseX, sliderX, sliderX + sliderWidth, 
            minVal, maxVal);
    }
}
