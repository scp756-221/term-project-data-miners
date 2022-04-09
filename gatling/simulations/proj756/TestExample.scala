
import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class RecordedSimulation extends Simulation {

  private val httpProtocol = http
    .baseUrl("http://computer-database.gatling.io")
    .inferHtmlResources(AllowList(), DenyList(""".*\.js""", """.*\.css""", """.*\.gif""", """.*\.jpeg""", """.*\.jpg""", """.*\.ico""", """.*\.woff""", """.*\.woff2""", """.*\.(t|o)tf""", """.*\.png""", """.*detectportal\.firefox\.com.*"""))
    .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    .acceptEncodingHeader("gzip, deflate")
    .acceptLanguageHeader("en-GB,en-US;q=0.9,en;q=0.8")
    .upgradeInsecureRequestsHeader("1")
    .userAgentHeader("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36")

  object Search{
    val seachFeeder = csv("resources/search.csv").random
    val search = exec(
      http("Load_Homepage")
        .get("/computers")
    )
    .pause(2)
    .feed(seachFeeder)
    .exec(
      http("Search_Computer_${searchCriterion}")
        .get("/computers?f=${searchCriterion}")
        .check(css("a:contains('${searchComputerName}')", "href").saveAs("computerURL")))
    .pause(2)
    .exec(
      http("Select_Computer_${searchComputerName}")
        .get("${computerURL}")
    )
    .pause(2)
  }

  object Browse{
    val browse = 
    repeat(times=5, counterName="i"){
      exec(http("Browser_Page_${i}")
      .get("/computers?p=${i}"))
      .pause(2)
    }
  }

  object Create{
    val computerFeeder = csv("resources/computers.csv").circular
    val create = exec(http("Load_Create_Computer_Page")
        .get("/computer/new"))
        .pause(2)
        .feed(computerFeeder)
        .exec(http("Create_Computer_${computerName}")
        .post("/computers")
        .formParam("name", "${computerName}")
        .formParam("introduced", "${introduced}")
        .formParam("discontinued", "${discontinued}")
        .formParam("company", "${companyId}")
        .check(status.is(200))
    )
  }
  
    
  val admins = scenario("Admins").exec(Search.search, Browse.browse, Create.create)

  val users = scenario("Users").exec(Search.search, Browse.browse)

	setUp(admins.inject(atOnceUsers(5)),
        users.inject(
          nothingFor(5),
          atOnceUsers(1),
          rampUsers(5) during (10),
          constantUsersPerSec(20) during (20)
          )).protocols(httpProtocol)
}
