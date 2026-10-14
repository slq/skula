plugins {
    id("com.android.application")
    id("com.chaquo.python")
}
android {
    namespace = "pl.skula.android"
    compileSdk = 35
    defaultConfig {
        applicationId = "pl.skula.android"
        minSdk = 26
        targetSdk = 35
        versionCode = providers.gradleProperty("skulaVersionCode").orElse("23").get().toInt()
        versionName = providers.gradleProperty("skulaVersionName").orElse("0.15.0").get()
        ndk { abiFilters += listOf("arm64-v8a", "x86_64") }
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    sourceSets.getByName("androidTest").assets.srcDir(rootProject.file(".tools/update-test-assets"))
    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("debug") // Reuse the local signing configuration; the new application ID requires backup/import.
        }
    }
}
chaquopy {
    defaultConfig {
        version = "3.13"
        val configuredPython = providers.gradleProperty("buildPython").orNull
        if (configuredPython != null) buildPython(configuredPython)
        pip { install("-r", "requirements-android.txt") }
    }
}
dependencies {
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test:runner:1.7.0")
    androidTestImplementation("androidx.test:core:1.7.0")
    androidTestImplementation("junit:junit:4.13.2")
}
