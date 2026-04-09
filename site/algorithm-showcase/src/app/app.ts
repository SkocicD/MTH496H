import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface Point {
  x: number;
  y: number;
}
interface Segment {
  p1: Point;
  p2: Point;
}
interface DelaunayResponse {
  segments: Segment[];
}
interface VoronoiResponse {
  segments: Segment[];
}
interface CrustResponse {
  segments: Segment[];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements AfterViewInit {
  constructor(private http: HttpClient) { }

  @ViewChild('canvas', { static: true }) canvasRef!: ElementRef<HTMLCanvasElement>;

  private ctx!: CanvasRenderingContext2D;
  // private api_url = "http://127.0.0.1:8000";
  private api_url = "https://mth496h.onrender.com";


  // Coordinate system
  private originX!: number;
  private originY!: number;
  private scale = 50;

  private points: Point[] = [];
  private delaunay_edges: Segment[] = [];
  private voronoi_edges: Segment[] = [];
  private crust_edges: Segment[] = [];
  private activeButtons: Set<string> = new Set();

  getButtonClass(name: string, color: string) {
    const isActive = this.activeButtons.has(name);

    const base = "px-4 py-2 rounded text-white transition";

    const colors: any = {
      blue: isActive ? "bg-blue-700" : "bg-blue-500 hover:bg-blue-600",
      green: isActive ? "bg-green-700" : "bg-green-500 hover:bg-green-600",
      red: isActive ? "bg-red-700" : "bg-red-500 hover:bg-red-600",
      purple: isActive ? "bg-purple-700" : "bg-purple-500 hover:bg-purple-600"
    };

    return `${base} ${colors[color]}`;
  }

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

      // Add the rescaled point to the list
      this.points.push(this.screenToWorld(screenX, screenY));
      // reset the delaunay edges.
      this.delaunay_edges = [];
      this.voronoi_edges = [];
      this.crust_edges = [];


      if (this.activeButtons.has('delaunay')) {
        this.handleDelaunay()
      }
      if (this.activeButtons.has('voronoi')) {
        this.handleVoronoi()
      }
      if (this.activeButtons.has('crust')) {
        this.handleCrust()
      }

      this.redraw();
    });
  }

  private handleDelaunay() {
    this.http.post<DelaunayResponse>(
      this.api_url + '/delaunay',
      { points: this.points }
    ).subscribe(response => {
      this.delaunay_edges = response.segments;
      this.redraw();
    });
  }

  private handleVoronoi() {
    this.http.post<VoronoiResponse>(
      this.api_url + '/voronoi',
      { points: this.points }
    ).subscribe(response => {
      this.voronoi_edges = response.segments;
      this.redraw();
    });
  }

  private handleCrust() {
    this.http.post<CrustResponse>(
      this.api_url + '/crust',
      { points: this.points }
    ).subscribe(response => {
      this.crust_edges = response.segments;
      this.redraw();
    });
  }

  private setupResizeEvents(canvas: HTMLCanvasElement) {
    window.addEventListener('resize', () => {
      const rect = canvas.getBoundingClientRect();

      canvas.width = rect.width;
      canvas.height = rect.height;

      // Bottom-left origin
      this.originX = 0;
      this.originY = canvas.height;
      this.delaunay_edges = [];

      this.redraw();
    });
  }

  private redraw() {
    const canvas = this.canvasRef.nativeElement;
    // clear canvas
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw the points
    for (const point of this.points) {
      this.drawPointWorld(point.x, point.y);
    }

    //draw the lines
    for (const line of this.delaunay_edges) {
      this.drawLineWorld(
        line.p1.x,
        line.p1.y,
        line.p2.x,
        line.p2.y,
        'green'
      );
    }

    for (const line of this.voronoi_edges) {
      this.drawLineWorld(
        line.p1.x,
        line.p1.y,
        line.p2.x,
        line.p2.y,
        'red'
      );
    }

    for (const line of this.crust_edges) {
      this.drawLineWorld(
        line.p1.x,
        line.p1.y,
        line.p2.x,
        line.p2.y,
        'purple'
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

  private drawLine(x1: number, y1: number, x2: number, y2: number, color: string = 'black') {
    this.ctx.beginPath();
    this.ctx.strokeStyle = color;
    this.ctx.moveTo(x1, y1);
    this.ctx.lineTo(x2, y2);
    this.ctx.stroke();
  }

  private drawLineWorld(x1: number, y1: number, x2: number, y2: number, color: string = 'black') {
    const p1 = this.worldToScreen(x1, y1);
    const p2 = this.worldToScreen(x2, y2);
    this.drawLine(p1.x, p1.y, p2.x, p2.y, color);
  }

  // ---------------------------
  // Buttons
  // ---------------------------
  //
  toggle(name: string) {
    if (this.activeButtons.has(name)) {
      this.activeButtons.delete(name);
      if (name === 'delaunay') {
        this.delaunay_edges = [];
      } else if (name === 'voronoi') {
        this.voronoi_edges = [];
      } else if (name === 'crust') {
        this.crust_edges = [];
      }
      this.redraw();
    } else {
      this.activeButtons.add(name);
      if (name === 'delaunay') {
        this.handleDelaunay();
      } else if (name === 'voronoi') {
        this.handleVoronoi();
      } else if (name === 'crust') {
        this.handleCrust();
      }
    }
  }
}
