amends "pkl:Project"

dependencies {
  ["uri"] { uri = "package://pkg.pkl-lang.org/pkl-pantry/pkl.experimental.uri@1.0.3#/URI.pkl" }
}

package {
  name = "schema.org.experimental" 
  version = "{{schemaorg_version}}" 
  importUri = "modulepath:/pkl/"
  authors {
    "pkl@captnemo.in"
  }
  license =  "MIT"
  exclude = "src"

  sourceCode = "https://github.captnemo.in/pkl-schemaorg"
  issueTracker = "https://github.captnemo.in/pkl-schemaorg/issues"
  sourceCodeUrlScheme = "https://github.com/captn3m0/pkl-schemaorg/blob/v\(version)%{path}#L%{line}-L%{endLine}"
  documentation: "https://captnemo.in/pkl-schemaorg/"
}