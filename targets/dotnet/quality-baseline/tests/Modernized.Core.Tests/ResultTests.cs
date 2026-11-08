using System;
using Xunit;

namespace Modernized.Core.Tests;

public sealed class ResultTests
{
    private static readonly Error _alreadyPosted = new("Invoice.AlreadyPosted", "The invoice is already posted.");

    [Fact]
    public void A_success_carries_its_value_and_no_error()
    {
        Result<decimal> result = 12.50m;

        Assert.True(result.IsSuccess);
        Assert.Equal(12.50m, result.Value);
        Assert.Equal(Error.None, result.Error);
    }

    [Fact]
    public void A_failure_carries_its_error_and_refuses_its_value()
    {
        var result = Result.Failure<decimal>(_alreadyPosted);

        Assert.True(result.IsFailure);
        Assert.Equal(_alreadyPosted, result.Error);
        Assert.Throws<InvalidOperationException>(() => result.Value);
    }

    [Fact]
    public void A_failure_without_an_error_is_refused()
    {
        Assert.Throws<ArgumentException>(() => Result.Failure(Error.None));
    }
}
