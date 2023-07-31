var gulp = require('gulp'),
    markdown = require('gulp-remarkable'),
    frontMatter = require('gulp-front-matter'),
    layout = require('gulp-layout');
    argv = require('yargs').argv;

var inputDir = argv.input_dir;
var outputDir = argv.output_dir;

gulp.task('Convert Markdown to HTML', function () {
    return gulp.src(inputDir)
        .pipe(frontMatter())
        .pipe(markdown({
            html: true
        }))
        .pipe(layout(function (file) {
            return file.frontMatter;
        }))
        .pipe(gulp.dest(outputDir));
});