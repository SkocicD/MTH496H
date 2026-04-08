import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements AfterViewInit {

  @ViewChild('canvas', { static: true }) canvasRef!: ElementRef<HTMLCanvasElement>;

  private ctx!: CanvasRenderingContext2D;

  // Coordinate system
  private originX!: number;
  private originY!: number;
  private scale = 50;

  private lastPoint: { x: number; y: number } | null = null;
  private points: { x: number; y: number }[] = [];
  private lines: { p1: { x: number; y: number }, p2: { x: number; y: number } }[] = [];

  ngAfterViewInit() {
    const canvas = this.canvasRef.nativeElement;

    this.resizeCanvas(canvas);

    this.ctx = canvas.getContext('2d')!;

    this.originX = 0;
    this.originY = canvas.height;

    this.setupMouseEvents(canvas);
    this.setupResizeEvents(canvas);
  }

  private resizeCanvas(canvas: HTMLCanvasElement) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight - 70;
  }

  private setupMouseEvents(canvas: HTMLCanvasElement) {
    canvas.addEventListener('click', (event) => {
      const rect = canvas.getBoundingClientRect();

      const screenX = event.clientX - rect.left;
      const screenY = event.clientY - rect.top;

      // get the point in our coordinate system
      const world = this.screenToWorld(screenX, screenY);
      console.log("World coords:", world);
      this.points.push(world)

      if (this.lastPoint) {
        this.lines.push(
          {
            p1: this.lastPoint,
            p2: world
          }
        )
      }

      this.lastPoint = world;
      this.redraw();
    });
  }

  private setupResizeEvents(canvas: HTMLCanvasElement) {
    window.addEventListener('resize', () => {
      const rect = canvas.getBoundingClientRect();
      console.log("here");

      canvas.width = rect.width;
      canvas.height = rect.height;

      // Bottom-left origin
      this.originX = 0;
      this.originY = canvas.height;
      this.redraw();
    });
  }

  private redraw() {
    const canvas = this.canvasRef.nativeElement;
    console.log(canvas.height, canvas.width);
    // clear canvas
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw the points
    for (const point of this.points) {
      this.drawPointWorld(point.x, point.y);
    }

    //draw the lines
    for (const line of this.lines) {
      this.drawLineWorld(
        line.p1.x,
        line.p1.y,
        line.p2.x,
        line.p2.y,
      );
    }
  }

  // ---------------------------
  // Coordinate transforms
  // ---------------------------

  private screenToWorld(x: number, y: number) {
    return {
      x: (x - this.originX) / this.scale,
      y: (this.originY - y) / this.scale
    };
  }

  private worldToScreen(x: number, y: number) {
    return {
      x: this.originX + x * this.scale,
      y: this.originY - y * this.scale
    };
  }

  // ---------------------------
  // Drawing
  // ---------------------------

  private drawPoint(x: number, y: number) {
    this.ctx.beginPath();
    this.ctx.arc(x, y, 3, 0, 2 * Math.PI);
    this.ctx.fill();
  }

  private drawPointWorld(x: number, y: number) {
    const p = this.worldToScreen(x, y);
    this.drawPoint(p.x, p.y);
  }

  private drawLine(x1: number, y1: number, x2: number, y2: number) {
    this.ctx.beginPath();
    this.ctx.moveTo(x1, y1);
    this.ctx.lineTo(x2, y2);
    this.ctx.stroke();
  }

  private drawLineWorld(x1: number, y1: number, x2: number, y2: number) {
    const p1 = this.worldToScreen(x1, y1);
    const p2 = this.worldToScreen(x2, y2);
    this.drawLine(p1.x, p1.y, p2.x, p2.y);
  }

  // ---------------------------
  // Buttons
  // ---------------------------

  onButton1() {
    console.log("Button 1");
  }

  onButton2() {
    console.log("Button 2");
  }

  onButton3() {
    console.log("Button 3");
  }
}
