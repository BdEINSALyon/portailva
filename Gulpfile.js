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

const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

// PostCSS plugins used
const postcssPlugins = [
    autoprefixer({ browsers: ['last 2 versions', '> 1%', 'ie >= 9'] }),
    cssnano(),
];

// Bootstrap SASS
var bootstrapSass = {
  src: 'node_modules/bootstrap-sass/'
};

// Sass options
var sassOpts = {
  in: 'assets/scss/main.scss',
  out: 'dist/css/',
  sassOpts: {
    includePaths: [bootstrapSass.src + 'assets/stylesheets'],
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
    gulp.src([
        require.resolve('jquery'),
        require.resolve('bootstrap-sass'),
        // Used by other scripts, must be first
    ], { base: '.' })
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(concat('script.js', { newline: ';\r\n' }))
        .pipe(uglify())
        .pipe(sourcemaps.write('.', { includeContent: true, sourceRoot: '../../' }))
        .pipe(gulp.dest('dist/js/')));


// Compiles the SCSS files to CSS
gulp.task('css', ['css:sprite'], () =>
    gulp.src('assets/scss/main.scss')
        .pipe(sourcemaps.init())
        .pipe(sass(sassOpts.sassOpts))
        .pipe(postcss(postcssPlugins))
        .pipe(sourcemaps.write('.', { includeContent: true, sourceRoot: '../../assets/scss/' }))
        .pipe(gulp.dest('dist/css/')));

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