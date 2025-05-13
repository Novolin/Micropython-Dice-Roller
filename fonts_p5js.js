// THIS IS JUST TO HAVE SOMETHING TO SHIT
// INTO P5.JS SO I CAN TEST THINGS
// WHO KNOWS IF ILL NEED IT


let HMULT = 180
let VMULT = 320

function setup() {
  createCanvas(HMULT * 4, VMULT * 9);
  noStroke()
  noLoop()
}




function draw_3(offset_x = 0, offset_y = 0){
  
}

function draw_4(offset_x = 0, offset_y = 0){
  
}

function draw_5(offset_x = 0, offset_y = 0){
  
}

function draw_num(offset_x, offset_y, num){
  switch (num){
    case 0:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 60, 200)
      break;
    case 1:
      fill(255);
      rect(120 + offset_x,30 + offset_y,30,260);
      break;
    case 2:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 260)
      fill(0)
      rect(30 + offset_x, 60 + offset_y, 90, 60) 
      rect(60 + offset_x, 150 + offset_y, 120,110)
      break;
    case 3:
      fill(255)
      rect(30 + offset_x,30 + offset_y,120,260)
      fill(0)
      rect(30 + offset_x, 60 + offset_y, 90, 200)
      fill(255)
      rect(60 + offset_x, 120 + offset_y, 90, 30)
      break;
    case 4:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 90, 120)
      rect(120 + offset_x, 30 + offset_y, 30, 260)
      fill(0)
      rect(60 + offset_x, 30 + offset_y, 60,90)
      break;
    case 5:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 120, 60)
      rect(30 + offset_x, 150 + offset_y, 90,110)
      break;
    case 6:
      fill(255)
      rect(30 + offset_x, 60 + offset_y, 30,230)
      rect(30 + offset_x, 30 + offset_y, 60, 30)
      rect(60 + offset_x, 120 + offset_y, 90, 170)
      fill(0)
      rect(60 + offset_x, 150 + offset_y, 60,110)
      break;
    case 7:
      fill(255);
      rect(120 + offset_x,30 + offset_y,30,260);
      rect(30 + offset_x, 30 + offset_y, 120, 30)
      break;
    case 8:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 60, 60)
      rect(60 + offset_x, 150 + offset_y, 60, 110)
      break;
    case 9:
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 120)
      rect(120 + offset_x, 30 + offset_y, 30, 260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 60,60)
      break;
    case "A":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120, 260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 60, 60)
      rect(60 + offset_x, 150 + offset_y, 60, 140)
      break;
    case "B":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 100, 260)
      rect(30 + offset_x, 120 + offset_y, 120,150)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 40, 60)
      rect(60 + offset_x, 150 + offset_y, 60, 110)
      break;
    case "C":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120,260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 120,200)
      break;
    case "D":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 100,260)
      rect(120 + offset_x, 50 + offset_y, 30, 220)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 60,200)
      break;
    case "E":
      fill(255)
      rect(30 + offset_x,30 + offset_y,120,260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 90, 200)
      fill(255)
      rect(60 + offset_x, 120 + offset_y, 60, 30)
      break;
    case "F":
      fill(255)
      rect(30 + offset_x,30 + offset_y,120,260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 90, 230)
      fill(255)
      rect(60 + offset_x, 120 + offset_y, 60, 30)
      break;
    case "G":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 120,260)
      fill(0)
      rect(60 + offset_x, 60 + offset_y, 120,200)
      fill(255)
      rect(120 + offset_x, 120 + offset_y, 30,170)
      rect(90 + offset_x, 120 + offset_y, 60, 30)
      break;
    case "H":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 30, 260)
      rect(120 + offset_x, 30 + offset_y, 30, 260)
      rect(30 + offset_x, 120 + offset_y, 120, 30)
      break;
    case "I":
      fill(255)
      rect(90 + offset_x, 30 + offset_y, 30, 260)
      break
    case "J":
      fill(255)
      rect(120 + offset_x, 30 + offset_y, 30, 260)
      rect(30 + offset_x, 120 + offset_y, 120,170)
      fill(0)
      rect(60 + offset_x, 120 + offset_y, 60,140)
      break;
      case "K":
      fill(255)
      rect(30 + offset_x, 30 + offset_y, 30, 260)
    default:
      print("no")
      
  }
}

function draw() {
  background(0);
  let chars = [0,1,2,3,4,5,6,7,8,9,"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  for (i = 0; i < chars.length; i += 1){
    let hpos = i % 4
    let vpos = floor(i / 4)
    draw_num(hpos * HMULT, vpos * VMULT , chars[i])
  }
}