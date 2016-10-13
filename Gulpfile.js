const path = require('path');
const livereload = require('gulp-livereload');
const concat = require('gulp-concat');
const del = require('del');
const gulp = require('gulp');
const imagemin = require('gulp-imagemin');
const postcss = require('gulp-postcss');
const rename = require('gulp-rename');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const spritesmith = require('gulp.spritesmith');
const uglify = require('gulp-uglify');
const jshint = require('gulp-jshint');
const merge = require('merge-stream');
const order = require('gulp-order');

const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

// PostCSS plugins used
const postcssPlugins = [
  autoprefixer({ browsers: ['last 2 versions', '> 1%', 'ie >= 9'] }),
  cssnano(),
];

// Css vendors
const cssVendors = [
  'assets/css/datatables.bootstrap.css'
];

// JS vendors
const jsVendors = [
  'node_modules/jquery/dist/jquery.js',
  'node_modules/bootstrap-sass/assets/javascripts/bootstrap.js',
  'node_modules/datatables/media/js/jquery.dataTables.js',
  'assets/js/datatables.bootstrap.js',
  // Used by other scripts, must be first
  'assets/js/main.js'
];

// Sass Vendors
const sassVendors = [
  'node_modules/bootstrap-sass/assets/stylesheets',
  'node_modules/font-awesome/scss'
];

// Sass options
var sassOpts = {
  in: 'assets/scss/main.scss',
  out: 'dist/css/',
  sassOpts: {
    includePaths: sassVendors,
    sourceMapContents: true
  }
};

// Deletes the generated files
gulp.task('clean', () => del([
    'dist/',
    'assets/scss/_sprite.scss',
    'assets/images/sprite*.png',
]));

// Lint the js source files
gulp.task('js:lint', () =>
  gulp.src([
    'assets/js/*.js'
  ])
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(jshint.reporter('fail')));

// Concat and minify all the js files
gulp.task('js', () =>
  gulp.src(jsVendors, { base: '.' })
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(order(jsVendors, { base: './' }))
    .pipe(concat('script.js', { newline: ';\r\n' }))
    .pipe(uglify())
    .pipe(sourcemaps.write('.', { includeContent: true, sourceRoot: '../../' }))
    .pipe(gulp.dest('dist/js/')));


// Compiles the SCSS files to CSS
gulp.task('css', ['css:sprite', 'css:fonts'], () => {
  // Sass
  var sassStream = gulp.src('assets/scss/main.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(sassOpts.sassOpts))
    .pipe(concat('styles-sass.scss'));

  var vendorStream = gulp.src(cssVendors)
    .pipe(concat('styles-vendors.css'));

  var mergedStream = merge(sassStream, vendorStream)
    .pipe(concat('main.css'))
    .pipe(postcss(postcssPlugins))
    .pipe(sourcemaps.write('.', { includeContent: true, sourceRoot: '../../assets/scss/' }))
    .pipe(gulp.dest('dist/css/'));

  return mergedStream;
});

// Generates a sprite
gulp.task('css:sprite', () =>
  gulp.src('assets/images/sprite/*.png')
    .pipe(spritesmith({
      cssTemplate: 'assets/scss/_sprite.scss.hbs',
      cssName: 'scss/_sprite.scss',
      imgName: 'images/sprite.png',
      retinaImgName: 'images/sprite@2x.png',
      retinaSrcFilter: 'assets/images/sprite/*@2x.png',
    }))
    .pipe(gulp.dest('assets/')));

// Copy fonts
gulp.task('css:fonts', () =>
  gulp.src([
    'node_modules/font-awesome/fonts/*',
    'node_modules/bootstrap-sass/assets/fonts/**/*'
  ])
    .pipe(gulp.dest('dist/fonts/'))
);

// Optimizes the images
gulp.task('images', ['css:sprite'], () =>
  gulp.src('assets/{images,smileys}/*')
    .pipe(imagemin())
    .pipe(gulp.dest('dist/')));

// Watch for file changes
gulp.task('watch', ['build'], () => {
  gulp.watch('assets/js/*.js', ['js']);
  gulp.watch(['assets/{images,smileys}/**/*', '!assets/images/sprite*.png'], ['images']);
  gulp.watch(['assets/scss/**/*.scss', '!assets/scss/_sprite.scss'], ['css']);

  gulp.watch('dist/**/*', file =>
    livereload.changed(
      path.join('static/', path.relative(path.join(__dirname, 'dist/'), file.path))
    )
  );

  livereload.listen();
});

// Compiles errors' CSS
gulp.task('errors', () =>
  gulp.src('errors/scss/main.scss')
    .pipe(sourcemaps.init())
    .pipe(sass({ sourceMapContents: true, includePaths: 'assets/scss/' }))
    .pipe(postcss(postcssPlugins))
    .pipe(sourcemaps.write('.', { includeContent: true, sourceRoot: '../scss/' }))
    .pipe(gulp.dest('errors/css/')));

gulp.task('test', ['js:lint']);
gulp.task('build', ['css', 'js', 'images']);
gulp.task('default', ['watch', 'test']);