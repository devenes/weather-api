const app = require("express")();
const supertest = require("supertest");
const request = supertest(app);

app.get("/", function (req, res) {
    res.status(200).json({
        fistname: "Enes",
        lastname: "Turan"
    });
});

describe("GET /", function () {
    it("should return 200 OK", function (done) {
        request
            .get("/")
            .expect(200)
            .expect((response) => {
                expect(response.body).toEqual({
                    fistname: "Enes",
                    lastname: "Turan"
                });
            })
            .end(function (err, res) {
                if (err) return done(err);
                done();
            });
    });
});
