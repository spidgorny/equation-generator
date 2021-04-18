// graph_calc.js
//
// This is a quick and dirty way to graph mathematical functions expressed in
// JavaScript and rendered as SVG. The file example.html provides an example use
// case. It's important to call setCanvasSize before graphing with a call to
// drawFn.
//

const svg = document.getElementById('svg');
const svgNS = svg.namespaceURI;

const lightStyle = {stroke: '#ddd', fill: 'transparent', 'stroke-width': 3};
const darkStyle = (color: string = '#666') => ({stroke: color, fill: 'transparent', 'stroke-width': 3});

let xSize;
let ySize;

const numFnPts = 300;

function setCanvasSize(w, h) {
	xSize = w
	ySize = h
	addAttributes(svg, {width: xSize, height: ySize})
}

function add(eltName, attr) {
	const elt = document.createElementNS(svgNS, eltName);
	svg.appendChild(elt)
	if (attr) addAttributes(elt, attr)
	return elt
}

function addAttributes(elt, attr) {
	for (let key in attr) {
		elt.setAttribute(key, attr[key])
	}
	return elt
}

function drawFn(xMin, xMax, yMin, yMax, opts, fn) {

	if (opts && fn === undefined) {
		fn = opts
		opts = null
	}

	if (opts && opts.doEqualizeAxes) {
		// This means to *increase* the frame just enough so that the axes are
		// equally scaled.
		const xRatio = (xMax - xMin) / xSize;
		const yRatio = (yMax - yMin) / ySize;
		if (xRatio < yRatio) {
			const xMid = (xMax + xMin) / 2;
			var half = (xMax - xMin) / 2
			xMin = xMid - half * (yRatio / xRatio)
			xMax = xMid + half * (yRatio / xRatio)
		} else {
			const yMid = (yMax + yMin) / 2;
			var half = (yMax - yMin) / 2
			yMin = yMid - half * (xRatio / yRatio)
			yMax = yMid + half * (xRatio / yRatio)
		}
	}

	function canvasPtFromXY(x, y) {
		const xPerc = (x - xMin) / (xMax - xMin);
		const yPerc = (y - yMin) / (yMax - yMin);
		return [xPerc * xSize, ySize - yPerc * ySize]
	}

	function drawTickAroundPt(p, dir) {
		const tick = add('line', lightStyle);
		const a = [p[0], p[1]];
		a[dir] -= 5
		const b = [p[0], p[1]];
		b[dir] += 5
		addAttributes(tick, {x1: a[0], y1: a[1], x2: b[0], y2: b[1]})
	}

	if (opts && opts.doDrawAxes) {

		// The x-axis.
		const leftPt = canvasPtFromXY(xMin, 0);
		const rightPt = canvasPtFromXY(xMax, 0);
		if (0 <= leftPt[1] && leftPt[1] < ySize) {
			const xAxis = add('line', lightStyle);
			addAttributes(xAxis, {
				x1: leftPt[0], y1: leftPt[1],
				x2: rightPt[0], y2: rightPt[1]
			})
			for (var x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
				var p = canvasPtFromXY(x, 0)
				drawTickAroundPt(p, 1)  // 1 == vertical tick
			}
		}

		// The y-axis.
		const botPt = canvasPtFromXY(0, yMin);
		const topPt = canvasPtFromXY(0, yMax);
		if (0 <= botPt[0] && botPt[0] < xSize) {
			const yAxis = add('line', lightStyle);
			addAttributes(yAxis, {
				x1: botPt[0], y1: botPt[1],
				x2: topPt[0], y2: topPt[1]
			})
			for (var y = Math.ceil(yMin); y <= Math.floor(yMax); y++) {
				var p = canvasPtFromXY(0, y)
				drawTickAroundPt(p, 0)  // 0 == horizontal tick
			}
		}
	}

	const xDelta = (xMax - xMin) / (numFnPts - 1);
	const pts = [];
	let xPrev = xMin;
	let prevCanvasY = false;

	for (let i = 0; i < numFnPts; i++) {
		var x, xTarget = xMin + i * xDelta
		do {
			x = xTarget
			var y = fn(x)
			var canvasPt = canvasPtFromXY(x, y)
			let perc = 0.5;
			while (prevCanvasY && Math.abs(prevCanvasY - canvasPt[1]) > 30 &&
			perc > 0.0001) {
				x = (1 - perc) * xPrev + perc * xTarget
				var y = fn(x)
				var canvasPt = canvasPtFromXY(x, y)
				perc /= 2
			}
			pts.push(canvasPt[0], canvasPt[1])
			xPrev = x
			prevCanvasY = canvasPt[1]
		} while (x < xTarget);
	}

	const polyline = add('polyline', opts.color ? darkStyle(opts.color) : darkStyle());
	addAttributes(polyline, {points: pts.join(' ')})
}
