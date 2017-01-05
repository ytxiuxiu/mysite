var gulp = require('gulp');
var sass = require('gulp-ruby-sass');
var rename = require('gulp-rename');
var unzip = require('gulp-unzip');
var babelify = require('babelify');
var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var sourcemaps = require('gulp-sourcemaps');


var modules = ['home', 'travel'];

function handleSassError(err) {
  console.error('Sass Compiling Error', err.message);
}

// copy vendor css
gulp.task('css-vendor', function() {
  gulp.src([
    'bower_components/bootstrap/dist/css/bootstrap.css',
    'bower_components/normalize-css/normalize.css'
  ])
    .pipe(rename(function(path) {
        path.extname = '.scss'
    }))
    .pipe(gulp.dest('home/static/home/sass/vendor'));
});

// compile all css files
gulp.task('css', function() {
  for (var i = 0, l = modules.length; i < l; i++) {
    var module = modules[i];
    sass(module + '/static/' + module + '/sass/*.scss', {})
      .on('error', handleSassError)
      .pipe(gulp.dest(module + '/static/' + module + '/css'));
  }
});

// copy vendor js
gulp.task('js-vendor', function() {

});


gulp.task('js', function() {
  var bundler = browserify({ 
    entries: 'home/static/home/node/app.js',
    debug: true
  });

  bundler.transform(babelify, { presets: ['es2015', 'react'] });
  bundler.bundle()
    .on('error', function (err) { console.error(err); })
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))

    .pipe(sourcemaps.write(''))
    .pipe(gulp.dest('home/static/home/js'));
});

// unzip icons
gulp.task('icons', function() {
  gulp.src('home/static/home/icons.zip')
    .pipe(unzip())
    .pipe(gulp.dest('.tmp/icons'));
  gulp.src('.tmp/icons/style.css')
    .pipe(rename('icons.scss'))
    .pipe(gulp.dest('home/static/home/sass/vendor'))
  gulp.src('.tmp/icons/fonts/*.*')
    .pipe(gulp.dest('home/static/home/css/fonts'))
});

gulp.task('default', ['css-vendor', 'icons', 'css', 'js-vendor', 'js'], function() {
  for (var i = 0, l = modules.length; i < l; i++) {
    var module = modules[i];
    gulp.watch(module + '/static/' + module + '/sass/**/*.scss', ['css']);
  }
  gulp.watch('home/static/home/icons.zip', ['icons']);
  gulp.watch('home/static/home/node/**/*.js', ['js']);
});

gulp.task('build', ['css-vendor', 'icons', 'css', 'js-vendor', 'js'], function() {

});